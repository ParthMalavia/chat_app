import axios from "axios";
import { jwtDecode } from "jwt-decode";
import dayjs from "dayjs";
import { useContext } from "react";
import AuthContext from "../context/AuthContext";
import { AUTHTOKENS, BASE_URL } from "./enums";

/**
 * Custom hook to create and configure an axios instance
 * with authorization headers from localStorage.
 */
const UseAxios = () => {
    const { authTokens, setUser, setAuthTokens } = useContext(AuthContext);

    const axiosInstance = axios.create({
        baseURL: BASE_URL,
        headers: {
            Authorization: `Bearer ${authTokens?.access}`,
        },
    });

    /**
     * Intercept all requests and check if the access token
     * is still valid. If not, refresh it and retry the request.
     */
    axiosInstance.interceptors.request.use(
        async (req) => {
            const user = jwtDecode(authTokens.access);
            const isExpired = dayjs.unix(user.exp).diff(dayjs()) < 1;

            if (!isExpired) {
                return req;
            }

            const response = await axios.post(
                `${BASE_URL}/token/refresh/`,
                { refresh: authTokens.refresh }
            );
            localStorage.setItem(AUTHTOKENS, JSON.stringify(authTokens));
            setAuthTokens(response.data);
            setUser(jwtDecode(response.data.access));

            // Update headers with new access token
            req.headers.Authorization = `Bearer ${response.data.access}`;
            return req;
        }
    );

    return axiosInstance;
};

export default UseAxios;

