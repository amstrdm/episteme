import React from 'react';
import Favorites from '../components/Favorites';

const FavoritesPage = () => {
  return (
    <div className="rounded-2xl bg-widget-background p-6">
      <h2 className="text-2xl font-semibold text-white-text mb-4">
        My Favorites
      </h2>
      <Favorites />
    </div>
  );
};

export default FavoritesPage;