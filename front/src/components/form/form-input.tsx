import { FC } from 'react';
import './form.css';

interface Props {
    value: string;
    onChange: (value: string) => void;
    placeholder: string;
    type: string;
    disabled?: boolean;
    required?: boolean;
    label: string;
}

const FormInput: FC<Props> = ({
    value,
    onChange,
    placeholder,
    type,
    disabled,
    required,
    label
}) => (
    <div className='form-control'>
        <label>{label} <span className='form-required'>{required ? '*' : ''}</span></label>
        <input
            type={type}
            value={value}
            onChange={(event) => onChange(event.target.value)}
            disabled={disabled ?? false}
            placeholder={placeholder}
        />
    </div>
);

export default FormInput;
