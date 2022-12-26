import { FC } from 'react';
import './polarity-score.css'

interface Props {
    score: number;
}

const PolarityScore: FC<Props> = ({ score }) => {
    
    let polarityColor;

    console.log(score)

    if (score >= 5.5) polarityColor = 'green';
    else if (score >= 4) polarityColor = 'orange';
    else polarityColor = 'red';

    const barWidth = `load-${Math.floor(score) * 10}`;
    const style = `polarity-score ${polarityColor} ${barWidth}`;

    return (
        <div className='polarity-container'>
            <i className="fa-solid fa-face-sad-tear polarity-sad-icon"></i>
            <div className='polarity-bar'>
                <div className={style}></div>
            </div>
            <i className="fa-solid fa-face-laugh-beam polarity-happy-icon"></i>
        </div>
    );
};

export default PolarityScore;