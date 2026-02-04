/**
 * NewsListPage - Page component for displaying news list with data fetching.
 * [Feature: News Management] [Story: NM-PUBLIC-001] [Ticket: NM-PUBLIC-001-FE-T01]
 */
import { useSearchParams } from 'react-router-dom';
import { useNewsList } from '../hooks/useNewsList';
import { NewsList } from '../components/NewsList';
import { Pagination } from '../components/Pagination';

/**
 * NewsListPage - Public news list page with pagination.
 * [Feature: News Management] [Story: NM-PUBLIC-001] [Ticket: NM-PUBLIC-001-FE-T01]
 */
export function NewsListPage() {
  const [searchParams, setSearchParams] = useSearchParams();
  const page = parseInt(searchParams.get('page') || '1', 10);
  const pageSize = 10;

  const { data, isLoading, isError, error } = useNewsList({ page, pageSize });

  const handlePageChange = (newPage: number) => {
    setSearchParams({ page: newPage.toString() });
  };

  if (isError) {
    return (
      <main className="container mx-auto px-4 py-8">
        <div className="text-center py-12">
          <p className="text-red-600 dark:text-red-400">
            Error al cargar las noticias: {error?.message || 'Error desconocido'}
          </p>
        </div>
      </main>
    );
  }

  const totalPages = data ? Math.ceil(data.total / data.page_size) : 0;

  return (
    <main className="container mx-auto px-4 py-8">
      <header className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
          Noticias
        </h1>
        <p className="mt-2 text-gray-600 dark:text-gray-300">
          Últimas noticias de la comunidad
        </p>
      </header>

      <NewsList items={data?.items || []} isLoading={isLoading} />

      {totalPages > 1 && (
        <Pagination
          currentPage={page}
          totalPages={totalPages}
          onPageChange={handlePageChange}
          className="mt-8"
        />
      )}
    </main>
  );
}
