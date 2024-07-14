import { toast } from 'react-toastify';

const handleResponse = async (response: Response) => {
  if (!response.ok) {
    const errorData = await response.json();
    toast.error(errorData.message);
  }
  return response.json();
};

export default handleResponse;
