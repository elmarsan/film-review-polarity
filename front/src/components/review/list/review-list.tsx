import { FC, useEffect, useState } from 'react';
import { HttpAPI } from '../../../api/http-api';
import ReviewCard from '../card/review-card';
import { Review } from '../review';
import './review-list.css';


const ReviewList: FC = () => {
    const [reviews, setReviews] = useState<Array<Review>>([]);
    
    useEffect(() => {
        HttpAPI
        .fetchReviews()
        .then((reviewList) => setReviews(reviewList));
      }, [])
    
    return (
        <div className='review-list'>
        {
            reviews.map((review, i) => (
                <div className='review-item'>
                    <ReviewCard review={review} key={i}/>
                </div>
            ))
        }
        </div>
    );
};

export default ReviewList;