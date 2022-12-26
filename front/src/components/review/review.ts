export interface Review {
    film: string;
    name: string;
    body: string;
    author: string;
    modelScore: number;
    userScore?: number;
    date: Date;
}
