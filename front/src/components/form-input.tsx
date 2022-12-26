import { FC } from "react";

interface Props {
    value: string;
    onChange: (value: string) => void;
    placeholder: string;
    type: string;
    disabled?: boolean;
}

const FormInput: FC<Props> = ({
    value,
    onChange,
    placeholder,
    type,
    disabled
}) => (
    <input
        type={type}
        value={value}
        onChange={(event) => onChange(event.target.value)}
        disabled={disabled ?? false}
        placeholder={placeholder}
    />
);

export default FormInput;
