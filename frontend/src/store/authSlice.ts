import {
  createAsyncThunk,
  createSlice,
  isFulfilled,
  isPending,
  isRejected,
  PayloadAction,
} from '@reduxjs/toolkit';
import API_URLS from '../services/apiUrls';
import axios, { AxiosResponse } from 'axios';
import { toast } from 'react-toastify';

interface AuthState {
  token: string | null;
  isAuthenticated: boolean;
  loading: boolean;
  errorMessage: string | null;
}

const initialState: AuthState = {
  token: localStorage.getItem('token'),
  isAuthenticated: !!localStorage.getItem('token'),
  loading: false,
  errorMessage: null,
};

export const signUpApi = createAsyncThunk(
  'auth/signUpApi',
  async (body: any) => {
    const response: AxiosResponse<any> = await axios.post<any>(
      API_URLS.AUTH.CREATE_USER,
      body,
    );

    return {
      data: response.data,
      status: response.status,
    };
  },
);

export const signInApi = createAsyncThunk(
  'auth/signInApi',
  async (body: any) => {
    console.log(body)
    const response: AxiosResponse<any> = await axios.post<any>(
      API_URLS.AUTH.SIGN_IN_USER,
      body,
    );
    return {
      data: response.data,
      status: response.status,
    };
  },
);

export const clearAuthentication = () => (dispatch: any) => {
  dispatch(logout());
};

const authSlice = createSlice({
  name: 'auth',
  initialState,
  reducers: {
    setToken: (state, action: PayloadAction<string | null>) => {
      state.token = action.payload;
      state.isAuthenticated = !!action.payload;
      if (action.payload) {
        localStorage.setItem('token', action.payload);
      } else {
        localStorage.removeItem('token');
      }
    },
    logout: (state) => {
      state.token = null;
      state.isAuthenticated = false;
      localStorage.removeItem('token');
    },
  },
  extraReducers(builder) {
    builder
      // .addCase(signUpApi.fulfilled, (state) => {
      //   state.loading = false;
      // })
      .addMatcher(isFulfilled(signUpApi, signInApi), (state) => {
        state.errorMessage = null;
        state.loading = false;
      })
      .addMatcher(isPending(signUpApi), (state) => {
        state.loading = true;
      })
      .addMatcher(isRejected(signUpApi), (state) => {
        state.errorMessage = null;
        state.loading = false;
        toast.error(state.errorMessage);
      });
  },
});

export const { setToken, logout } = authSlice.actions;

export default authSlice.reducer;
