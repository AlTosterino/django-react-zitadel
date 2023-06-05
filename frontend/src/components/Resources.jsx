import { useState } from "react";
import { useAuth } from "oidc-react";

const BACKEND_ZITADEL_INTROSPECT_API = "http://localhost:8000/introspect";
const BACKEND_ZITADEL_LOCAL_API = "http://localhost:8000/local";
export default function Resources() {
  const { userData } = useAuth();
  console.log(userData);
  const isLoggedIn = userData !== null;
  const [response, setResponse] = useState({});
  const hitApi = (api_url, token) => {
    setResponse({ Please: "Wait" });
    fetch(api_url, {
      headers: { Authorization: `${userData.token_type} ${token}` },
    })
      .then((response) => response.json())
      .then((response) => setResponse(response))
      .catch((err) => setResponse(err));
  };

  if (isLoggedIn) {
    return (
      <div className="mt-5">
        <p> You are logged in.</p>
        <div>
          GOT FROM API (CHECK CONSOLE FOR ERRORS):{" "}
          <pre>{JSON.stringify(response, null, 2)}</pre>
        </div>
        <button
          type="button"
          className="btn btn-primary"
          onClick={() =>
            hitApi(BACKEND_ZITADEL_INTROSPECT_API, userData.access_token)
          }
        >
          Hit API (Zitadel Introspect)!
        </button>
        <button
          type="button"
          className="mx-2 btn btn-primary"
          onClick={() => hitApi(BACKEND_ZITADEL_LOCAL_API, userData.id_token)}
        >
          Hit API (Zitadel Local Auth)!
        </button>
      </div>
    );
  }
  return <div className="my-12">How did you ended up here?!</div>;
}
