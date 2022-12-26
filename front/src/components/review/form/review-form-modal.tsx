import { FC } from 'react';
import Modal from 'react-modal';
import ReviewForm from './review-form';
import './review-form-modal.css'

interface Props {
    show: boolean;
    onClose: () => void;
}

const ReviewFormModal: FC<Props> = ({
    show,
    onClose
}) => {
    return (
        <Modal
            isOpen={show}
            onRequestClose={onClose}
            className='modal'
            style={{ overlay: { backgroundColor: 'rgba(255, 255, 255, .40)' }}}
        >
            <i className="fa-solid fa-x close-icon" onClick={onClose}></i>
            <ReviewForm/>
        </Modal>
    );
};

export default ReviewFormModal;
