import { FC } from 'react';
import './form.css'

interface Props {
    value: string;
    onChange: (value: string) => void;
    placeholder: string;
    rows: number;
    disabled?: boolean;
    required?: boolean;
    label: string;
}

const FormTextarea: FC<Props> = ({
    value,
    onChange,
    placeholder,
    rows,
    disabled,
    label,
    required
}) => (
    <div className='form-control'>
        <label>{label} <span className='form-required'>{required ? '*' : ''}</span></label>
        <textarea
            value={value}
            onChange={(event) => onChange(event.target.value)}
            disabled={disabled ?? false}
            placeholder={placeholder}
            rows={rows}
        />
    </div>
);

export default FormTextarea;
