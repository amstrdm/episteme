from fastapi import APIRouter
from database.db import session_scope
from database.models.thesisai import Ticker, Post, Point
from sqlalchemy import func
from .retrieve_public_stock_info.stock_profile import get_stock_profile
from fastapi import Query

router = APIRouter()

@router.get("/retrieve-analysis")
def fetch_analysis(ticker: str, timezone: str = Query(..., description="Timezone (e.g. 'Europe/Berlin')")):
    with session_scope() as session:
        ticker_obj = session.query(Ticker).filter(func.lower(Ticker.symbol) == ticker.lower()).first()

        if not ticker_obj:
            return {"error": "Ticker not found"}
        
        fmp_profile = get_stock_profile(ticker, timezone)
        company_data = {
            "ticker": ticker_obj.symbol,
            "title": ticker_obj.name,
            "description": ticker_obj.description,
            "sentimentScore": ticker_obj.overall_sentiment_score,
            "logo": fmp_profile["logo"],
            "website": fmp_profile["website"],
            "price": fmp_profile["price"],
            "exchangeShortName": fmp_profile["exchangeShortName"],
            "mktCap": fmp_profile["mktCap"],
            "industry": fmp_profile["industry"],
            "earningsCallDate": fmp_profile["earningsCallDate"],
            "analystRating": fmp_profile["analystRating"],
            "forwardPE": fmp_profile["forwardPE"],
            "dcf": fmp_profile["dcf"],
            "beta": fmp_profile["beta"]
        }


        points_query = session.query(Point).filter(Point.ticker_id == ticker_obj.id).all()
        points_list = []

        for pt in points_query:
            post_obj = session.get(Post, pt.post_id)
            pt_data = {
                "content": pt.text,
                "sentimentScore": pt.sentiment_score,
                "postUrl": post_obj.link if post_obj else None,
                "postTitle": post_obj.title if post_obj else None,
                "postAuthor": post_obj.author if post_obj else None,
                "postSource": post_obj.source if post_obj else None,
                "postDate": post_obj.date_of_post if post_obj else None,
                "criticismExists": pt.criticism_exists,
                "criticisms": []
            }

            for crit in pt.criticisms:
                criticism_data = {
                    "content": crit.text,
                    "validityScore": crit.validity_score,
                    "commentUrl": crit.comment.link if crit.comment else None
                }
                pt_data["criticisms"].append(criticism_data)
            
            points_list.append(pt_data)
    
    return {"company": company_data, "points": points_list}

        

