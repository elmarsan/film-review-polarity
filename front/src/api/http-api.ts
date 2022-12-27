import { Review, ReviewCreateDTO } from '../components/review/review';

interface ApiReviewDTOResponse {
    film_name: string;
    review_name: string;
    body: string;
    author: string;
    model_score: number;
    user_score: number;
    date: Date;
}

export class HttpAPI {
    private static url = 'http://localhost/review'

    static async fetchReviews(): Promise<Array<Review>> {
        const response = await fetch(this.url);
        
        if (response.status !== 200) 
            throw new Error('An error ocurred while fetching reviews');

        const reviewDTOList: Array<ApiReviewDTOResponse> = await response.json();

        return reviewDTOList.map(review => ({
            film: review.film_name,
            name: review.review_name,
            author: review.author,
            body: review.body,
            date: review.date,
            modelScore: review.model_score,
            userScore: review.user_score
        }));
    }

    static async createReview(reviewCreateDTO: ReviewCreateDTO): Promise<Review> {
        const response = await fetch(this.url, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                film_name: reviewCreateDTO.film,
                review_name: reviewCreateDTO.name,
                body: reviewCreateDTO.body,
                author: reviewCreateDTO.author,
            })
        });

        if (response.status !== 201) 
            throw new Error('An error ocurred while creating review');

        const reviewDTO: ApiReviewDTOResponse = await response.json();
        return {
            film: reviewDTO.film_name,
            name: reviewDTO.review_name,
            author: reviewDTO.author,
            body: reviewDTO.body,
            date: reviewDTO.date,
            modelScore: reviewDTO.model_score,
            userScore: reviewDTO.user_score
        };
    }
}
