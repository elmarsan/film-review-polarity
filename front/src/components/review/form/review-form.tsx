import { FC, useState } from 'react';
import './review-form.css';
import FormInput from '../../form/form-input';
import FormTextarea from '../../form/form-textarea';

const ReviewForm: FC = () => {
    const [film, setFilm] = useState('');
    const [author, setAuthor] = useState('');
    const [title, setTitle] = useState('');
    const [body, setBody] = useState('');
  
    const enabled = film && title && body && body.length > 50;

    return (
        <div className='review-form'>
            <h2>Write your review (Spanish)</h2>
            <form>
                <FormInput  
                  value={film}
                  onChange={(value) => setFilm(value)}
                  type='text'
                  placeholder='Uno de los nuestros (Goodfellas)'
                  label='Film name'
                  required={true}
                />

                <FormInput  
                  value={title}
                  onChange={(value) => setTitle(value)}
                  type='text'
                  placeholder='Otro gran film de mafia'
                  label='Review title'
                  required={true}
                />

                <FormInput  
                  value={author}
                  onChange={(value) => setAuthor(value)}
                  type='text'
                  placeholder='Scorsese 78'
                  label='Author'
                />

                <FormTextarea
                  value={body}
                  onChange={(value) => setBody(value)}
                  rows={6}
                  placeholder='No me digan por qué, pero a De Niro y a Pesci este tipo de papeles les vienen como anillo al dedo. Interpretaciones formidables, incluida por supuesto la de Ray Liotta, que sorprende. Añádanle a la película un genial guión y un gran desarrollo de los acontecimientos. Una pega es que quizá sea un film demasiado benevolente con el sistema y sus justicia en algunos momentos. La otra es el increíble y paradójico gazapo de los cubos de la niña: cuando veas la película, o la vuelvas a ver, fíjate en las cosas tan extrañas que pasan con unos cubos de colores fosforitos que lleva una niña a una visita en la cárcel (no doy más detalles para no fastidiar nada de la trama). Observa los cambios de posiciones, apariciones y desapariciones...'
                  label='Write your review'
                  required={true}
                />

                <button 
                    type='submit' 
                    onSubmit={(e) => console.log('submit')}
                    disabled={!enabled}
                >
                    Send
                </button>
            </form>
        </div>
    );
};

export default ReviewForm;