export interface Book {
  id: string;
  title: string;
  author: string;
  publisher: string;
  year: string;
  size: string;
  extension: string;
  md5: string;
  download: string;
}

export interface SearchResponse {
  results: Book[];
  page: number;
  hasMore: boolean;
}
