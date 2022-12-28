import { FC, useEffect, useState } from 'react';
import { HttpAPI } from './api/http-api';
import './app.css';
import ReviewFormModal from './components/review/form/review-form-modal';
import ReviewList from './components/review/list/review-list';
import { Review } from './components/review/review';
import Layout from './layout/layout';


const App: FC = () => {
  const [showReviewModal, setShowReviewModal] = useState(false);
  const [reviews, setReviews] = useState<Array<Review>>([]);
    
  useEffect(() => {
      HttpAPI
      .fetchReviews()
      .then((reviewList) => setReviews(reviewList));
    }, [])

  return (
    <Layout>
      <ReviewFormModal
        show={showReviewModal}
        onClose={() => setShowReviewModal(false)}
        onCreate={(review) => setReviews([review, ...reviews])}
      />

      <div className='project-info'>
        <div>
          <p>This project was built in 2019 for a final course work. Since then it has had three versions, this one you are seeing now is the third and hopefully the final version.</p>
          <p>You might be wondering what is it about. Here you can write in Spanish language some film review. Behind this page there is a deep learning model that would try to do it best for figure out how positive/negative is your sentiment.</p>
          <p>I invite you to try it, notice that the model will have a better performance the more words your review has.</p>
          <p>
            <a href='#'>More about project...</a>
          </p>
        </div>
        <button type='button' onClick={() => setShowReviewModal(true)}>Write review</button>
      </div>

      <div className="last-reviews">
        <h2>Latest reviews</h2>
        <ReviewList reviews={reviews}/>
      </div>
    </Layout>
  );
}

export default App;
