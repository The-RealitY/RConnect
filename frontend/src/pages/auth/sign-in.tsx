import React from 'react';
import { Formik, Form, Field, ErrorMessage } from 'formik';
import * as Yup from 'yup';
import { signInApi } from '../../store/authSlice';
import { useAppDispatch } from '../../store';
import { Link, useNavigate } from 'react-router-dom';
import '../../styles/auth/sign-up.scss';

const Login: React.FC = () => {
  const dispatch = useAppDispatch();
  const navigate = useNavigate();

  const initialValues = {
    sys_username: '',
    sys_password: '',
  };

  const validationSchema = Yup.object({
    sys_username: Yup.string().required('Required'),
    sys_password: Yup.string().required('Required'),
  });

  const handleSubmit = async (values: typeof initialValues) => {
    dispatch(signInApi(values)).then((resultAction: any) => {
      if (signInApi.fulfilled.match(resultAction)) {
        navigate('/sign-in');
      }
    });
  };

  return (
    <div className="login-page">
      <div className="form">
        <Formik
          initialValues={initialValues}
          validationSchema={validationSchema}
          onSubmit={handleSubmit}
        >
          <Form className="register-form">
            <div className="input-utils">
              <Field
                type="text"
                id="sys_username"
                name="sys_username"
                placeholder="Enter User Name"
              />
              <ErrorMessage
                name="sys_username"
                component="div"
                className="error-msg"
              />
            </div>
            <div className="input-utils">
              <Field
                type="password"
                id="sys_password"
                name="sys_password"
                placeholder="Enter Password"
              />
              <ErrorMessage
                name="sys_password"
                component="div"
                className="error-msg"
              />
            </div>
            <button type="submit">Login</button>
            <p className="message">
              Create New User <Link to={`/sign-up`}>Sign Up</Link>
            </p>
          </Form>
        </Formik>
      </div>
    </div>
  );
};

export default Login;
