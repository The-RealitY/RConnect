import DOMPurify from 'dompurify';

export const sanitizeInput = (input: string): string => {
    return DOMPurify.sanitize(input);
};

// Use Sanitizer in a Component: Use the sanitizer utility in a component where you handle user input.
// const sanitizedValue = sanitizeInput(event.target.value);
// setUserInput(sanitizedValue);