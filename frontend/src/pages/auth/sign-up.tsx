import React from 'react';
import { Formik, Form, Field, ErrorMessage } from 'formik';
import * as Yup from 'yup';
import '../../styles/auth/sign-up.scss';
import { signUpApi } from '../../store/authSlice';
import { useAppDispatch } from '../../store';
import { Link, useNavigate } from 'react-router-dom';

const SignUp: React.FC = () => {
  const dispatch = useAppDispatch();
  const navigate = useNavigate();

  const initialValues = {
    sys_name: '',
    sys_email: '',
    sys_username: '',
    sys_password: '',
  };

  const validationSchema = Yup.object({
    sys_email: Yup.string().email('Invalid email address').required('Required'),
    sys_password: Yup.string().required('Required'),
    sys_name: Yup.string().required('Required'),
    sys_username: Yup.string().required('Required'),
  });

  const handleSubmit = (values: typeof initialValues) => {
    dispatch(signUpApi(values)).then((resultAction: any) => {
      if (signUpApi.fulfilled.match(resultAction)) {
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
                id="sys_name"
                name="sys_name"
                placeholder="Enter Name"
              />
              <ErrorMessage
                name="sys_name"
                component="div"
                className="error-msg"
              />
            </div>
            <div className="input-utils">
              <Field
                type="text"
                id="sys_username"
                name="sys_username"
                placeholder="Enter Username"
              />
              <ErrorMessage
                name="sys_username"
                component="div"
                className="error-msg"
              />
            </div>
            <div className="input-utils">
              <Field
                type="email"
                id="sys_email"
                name="sys_email"
                placeholder="Enter Email"
              />
              <ErrorMessage
                name="sys_email"
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
            <button type="submit">Register</button>
            <p className="message">
              Already registered?
              <Link  to={`/sign-in`}>
                Sign In
              </Link>
            </p>
          </Form>
        </Formik>
      </div>
    </div>
  );
};

export default SignUp;
