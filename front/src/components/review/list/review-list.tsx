import { FC } from 'react';
import ReviewCard from '../card/review-card';
import { Review } from '../review';
import './review-list.css';

interface Props {
    reviews: Array<Review>
}

const ReviewList: FC<Props> = ({ reviews }) => {
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