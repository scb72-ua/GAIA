/**
 * App layout with navigation header.
 * [Feature: News Management] [Story: NM-PUBLIC-001] [Ticket: NM-PUBLIC-001-FE-T01]
 */
import { Outlet, Link } from 'react-router-dom';
import { Newspaper } from 'lucide-react';

export function AppLayout() {
  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-950">
      <header className="bg-white dark:bg-gray-900 border-b border-gray-200 dark:border-gray-800">
        <div className="container mx-auto px-4">
          <nav className="flex items-center h-16">
            <Link to="/" className="flex items-center gap-2 font-bold text-xl text-gray-900 dark:text-white">
              <Newspaper className="h-6 w-6 text-blue-600" />
              <span>GAIA</span>
            </Link>
            
            <ul className="ml-8 flex items-center gap-6">
              <li>
                <Link
                  to="/noticias"
                  className="text-gray-600 hover:text-gray-900 dark:text-gray-300 dark:hover:text-white transition-colors"
                >
                  Noticias
                </Link>
              </li>
            </ul>
          </nav>
        </div>
      </header>
      
      <Outlet />
    </div>
  );
}
