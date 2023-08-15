import {createContext, ReactNode, useContext, useState} from "react";

type UserContextType = {
  jwt: string | undefined;
  email: string | undefined;
  userId: string | undefined;
  setJwt: (
    jwt: string | undefined,
  ) => boolean;
  setJwtFromStorage: () => boolean;
};

const userContextDefaultValues: UserContextType = getDefaultUserContextValues();

function getDefaultUserContextValues(): UserContextType {
  return {
    jwt: undefined,
    email: undefined,
    userId: undefined,
    setJwt: () => {
      return false
    },
    setJwtFromStorage: () => {
      return false
    }
  }
}

const UserContext = createContext<UserContextType>(userContextDefaultValues);

export function useUser() {
  return useContext(UserContext);
}


type Props = {
  children: ReactNode;
};

export function UserProvider({children}: Props) {

  const [jwt, setJwt] = useState<string | undefined>(undefined);
  const [email, setEmail] = useState<string | undefined>(undefined);
  const [userId, setUserId] = useState<string | undefined>(undefined);


  const setNewJwt = (
    jwt: string | undefined,
  ): boolean => {
    if (!jwt) return false
    try {
      const jwtPayload = parseJwt(jwt)
      if (jwtPayload.sub) {
        setJwt(jwt)
        setUserId(jwtPayload.sub)
        if (jwtPayload.email) {
          setEmail(jwtPayload.email)
        }
        window.localStorage.setItem("jwt", jwt)
        return true
      }
    } catch (e) {
      console.log("jwt parsing error")
    }
    return false
  };

  const setJwtFromStorage = (): boolean => {
    const localstorageJwt = window.localStorage.getItem("jwt")
    if (localstorageJwt) {
      return setNewJwt(localstorageJwt)
    }
    return false
  }

  function parseJwt(token: string) {
    const base64Url = token.split('.')[1];
    const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    const jsonPayload = decodeURIComponent(window.atob(base64).split('').map(function (c) {
      return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
    }).join(''));

    return JSON.parse(jsonPayload);
  }

  const value: UserContextType = {
    jwt,
    email: email,
    userId: userId,
    setJwt: setNewJwt,
    setJwtFromStorage,
  };

  return (
    <>
      <UserContext.Provider value={value}>
        {children}
      </UserContext.Provider>
    </>
  );
}
