import { jwtDecode } from "jwt-decode";

interface DecodedToken {
  scopes?: string[];
}

export const getScopesFromToken = (token: string | null): string[] => {
  if (!token) return [];

  try {
    const decoded = jwtDecode<DecodedToken>(token);
    console.log("Token décodé :", decoded);
    return decoded.scopes || [];
  } catch {
    return [];
  }
};
