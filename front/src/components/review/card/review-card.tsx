import { FC } from 'react';
import PolarityScore from '../polarity-score/polarity-score';
import { Review } from '../review';
import './review-card.css';

const ReviewCard: FC<{review: Review}> = ({ review }) => (
    <div className='review-card'>
        <div className='review-card-header'>
            <h2>{review.film}</h2> 
            <div className='review-card-header-subtitle'>
                <span>{review.author}:</span> <h3>"{review.name}"</h3>
            </div>
        </div>
        <div className='review-card-body'>
            <h4>{review.date}</h4>
            <div>{review.body}</div>
        </div>
        <div className='review-card-footer'>
            <div className='review-card-footer-header'>
                <h4>Model score:</h4> <span>{review.modelScore.toFixed(2)}</span>
            </div>
            <PolarityScore score={review.modelScore}/>
        </div>
    </div>
);

export default ReviewCard;