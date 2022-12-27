import { FC } from 'react';

interface Props {
    value: string;
    onChange: (value: string) => void;
    placeholder: string;
    rows: number;
    disabled?: boolean;
}

const FormTextarea: FC<Props> = ({
    value,
    onChange,
    placeholder,
    rows,
    disabled
}) => (
    <textarea
        value={value}
        onChange={(event) => onChange(event.target.value)}
        disabled={disabled ?? false}
        placeholder={placeholder}
        rows={rows}
    />
);

export default FormTextarea;
