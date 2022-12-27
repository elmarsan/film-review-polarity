import { FC, useState } from 'react';
import './review-form.css';
import FormInput from '../../form/form-input';
import FormTextarea from '../../form/form-textarea';
import { HttpAPI } from '../../../api/http-api';
import { toast } from 'react-toastify';

interface Props {
  onSubmit: () => void;
}

const ReviewForm: FC<Props> = ({ onSubmit }) => {
    const [film, setFilm] = useState('');
    const [author, setAuthor] = useState('');
    const [name, setName] = useState('');
    const [body, setBody] = useState('');
  
    const enabled = film && name && body && body;

    const handleSubmit = async () => {
      await toast.promise(
        HttpAPI.createReview({
          film,
          author,
          name,
          body
        }),
        {
          pending: 'Creating review...',
          success: 'Review created successfully',
          error: 'Error while creating review'
        }
    );

      onSubmit();
    };

    return (
        <div className='review-form'>
            <h2>Write your review (Spanish)</h2>
            <form onSubmit={(e) => {
              e.preventDefault()
              handleSubmit();
            }}>
                <FormInput  
                  value={film}
                  onChange={(value) => setFilm(value)}
                  type='text'
                  placeholder='Uno de los nuestros (Goodfellas)'
                  label='Film name'
                  required={true}
                />

                <FormInput  
                  value={name}
                  onChange={(value) => setName(value)}
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

                <button type='submit' disabled={!enabled}>Send</button>
            </form>
        </div>
    );
};

export default ReviewForm;