import { FC } from 'react';
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

  return (
    <Layout>
        {/* <ReviewForm/> */}
        <ReviewList reviews={reviews}/>
    </Layout>
  );
}

export default App;
