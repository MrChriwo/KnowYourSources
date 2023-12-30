export interface requestBody {
    title: string;
    abstract: string;
}

export interface responseBody {
    title: string;
    category: string;
    doi: string
    authors: string;
    abstract: string;
    score: number;
}