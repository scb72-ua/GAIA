/**
 * App router configuration.
 * [Feature: News Management] [Story: NM-PUBLIC-001] [Ticket: NM-PUBLIC-001-FE-T01]
 */
import { createBrowserRouter, Navigate } from 'react-router-dom';
import { AppLayout } from '@/app/layout/AppLayout';
import { NewsListPage } from '@/features/news';

export const router = createBrowserRouter([
  {
    path: '/',
    element: <AppLayout />,
    children: [
      {
        index: true,
        element: <Navigate to="/noticias" replace />,
      },
      {
        path: 'noticias',
        element: <NewsListPage />,
      },
    ],
  },
]);
