/**
 * Pagination component.
 * [Feature: News Management] [Story: NM-PUBLIC-001] [Ticket: NM-PUBLIC-001-FE-T01]
 */
import { ChevronLeft, ChevronRight } from 'lucide-react';
import { cn } from '@/lib/utils';

interface PaginationProps {
  currentPage: number;
  totalPages: number;
  onPageChange: (page: number) => void;
  className?: string;
}

export function Pagination({
  currentPage,
  totalPages,
  onPageChange,
  className,
}: PaginationProps) {
  const canGoPrevious = currentPage > 1;
  const canGoNext = currentPage < totalPages;

  return (
    <nav
      className={cn('flex items-center justify-center gap-2', className)}
      aria-label="Navegación de páginas"
    >
      <button
        onClick={() => onPageChange(currentPage - 1)}
        disabled={!canGoPrevious}
        className={cn(
          'flex items-center gap-1 px-3 py-2 rounded-md text-sm font-medium transition-colors',
          canGoPrevious
            ? 'bg-white hover:bg-gray-100 text-gray-700 border dark:bg-gray-800 dark:hover:bg-gray-700 dark:text-gray-200 dark:border-gray-700'
            : 'bg-gray-100 text-gray-400 cursor-not-allowed dark:bg-gray-800 dark:text-gray-600'
        )}
        aria-label="Página anterior"
      >
        <ChevronLeft className="h-4 w-4" />
        <span>Anterior</span>
      </button>

      <span className="px-4 py-2 text-sm text-gray-600 dark:text-gray-300">
        Página {currentPage} de {totalPages}
      </span>

      <button
        onClick={() => onPageChange(currentPage + 1)}
        disabled={!canGoNext}
        className={cn(
          'flex items-center gap-1 px-3 py-2 rounded-md text-sm font-medium transition-colors',
          canGoNext
            ? 'bg-white hover:bg-gray-100 text-gray-700 border dark:bg-gray-800 dark:hover:bg-gray-700 dark:text-gray-200 dark:border-gray-700'
            : 'bg-gray-100 text-gray-400 cursor-not-allowed dark:bg-gray-800 dark:text-gray-600'
        )}
        aria-label="Página siguiente"
      >
        <span>Siguiente</span>
        <ChevronRight className="h-4 w-4" />
      </button>
    </nav>
  );
}
