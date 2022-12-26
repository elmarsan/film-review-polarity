import { FC, useState } from 'react';
import './app.css';
import ReviewFormModal from './components/review/form/review-form-modal';
import ReviewList from './components/review/list/review-list';
import { Review } from './components/review/review';
import Layout from './layout/layout';

const App: FC = () => {

  const review: Review = {
    film: 'OldBoy',
    author: 'elmarsan',
    body: `
      Me estoy empezando a aficionar al cine oriental, ya que me lo recomiendan muchas de mis almas gemelas y la verdad es que me está sorprendiendo gratamente.

      Old Boy es una película sencillamente brutal, como he leído en otras críticas.

      Al principio me resultó insípida, le faltaba algún ingrediente y no sabía cual. Pero poco a poco me fui metiendo en la historia y me supo enganchar hasta el punto de sufrir por todos y cada uno de los personajes, desde el técnicamente "malo", hasta el supuestamente "inocente".
      Escenas significativas, frases memorables, personajes carismáticos...

      Te envuelve en su originalidad y te fascina en su final.
    `,
    date: new Date(),
    modelScore: (Math.random() * 10),
    userScore: Math.random() * 10,
    name: 'Probably one of the best films ever'
  }

  const reviews: Array<Review> = [];

  for(let i = 0; i< 5; i++) {
    reviews.push(review)
  }

  const [showReviewModal, setShowReviewModal] = useState(false);

  return (
    <Layout>
        <ReviewFormModal 
          show={showReviewModal}
          onClose={() => setShowReviewModal(false)}
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

        <ReviewList reviews={reviews}/>
    </Layout>
  );
}

export default App;
