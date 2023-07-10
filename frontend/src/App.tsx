import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import SitesInfo from './SitesInfo';
import AddSite from './AddSite';
import './app.css';

function App() {
  const queryClient = new QueryClient();
  const queryString = window.location.search;
  const urlParams = new URLSearchParams(queryString);

  return (
    <QueryClientProvider client={queryClient}>
      <div className="container admin mt-5 mb-5 p-4">
        <nav className="navbar navbar-expand-lg navbar-light">
          <div className="container-fluid">
            <div className="container-fluid text-center logo">
              <a className="navbar-brand" href="/">
                <img
                  src="/++resource++plone-logo.svg"
                  width="215"
                  height="56"
                  alt="Plone logo"
                />
              </a>
            </div>
            <form id="topForm" className="d-flex"></form>
          </div>
        </nav>

        {urlParams.get('distribution') ? (
          <AddSite distribution={urlParams.get('distribution') || ''} />
        ) : (
          <>
            <SitesInfo />
          </>
        )}
      </div>
    </QueryClientProvider>
  );
}

export default App;
