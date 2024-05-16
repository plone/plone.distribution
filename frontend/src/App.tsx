import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import SitesInfo from './SitesInfo';
import AddSite from './AddSite';
import './app.css';
import '@plone/components/dist/basic.css';

function App() {
  const queryClient = new QueryClient();
  const queryString = window.location.search;
  const urlParams = new URLSearchParams(queryString);

  window.onload = () => {
    document.getElementById('root')?.classList.add('show-content');
  };

  return (
    <>
      <QueryClientProvider client={queryClient}>
        <div className="container admin">
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
      <div className="footer">
        <div className="footer-message">
          The Plone<sup>®</sup> Open Source CMS/WCM is{' '}
          <abbr title="Copyright">©</abbr> 2000-2024 by the{' '}
          <a className="item" href="http://plone.org/foundation">
            Plone Foundation
          </a>{' '}
          and friends. <br /> Distributed under the{' '}
          <a
            className="item"
            href="http://creativecommons.org/licenses/GPL/2.0/"
          >
            GNU GPL license
          </a>
          .
        </div>
        <ul className="links-list">
          <li className="item">
            <a
              className="item"
              href="https://docs.plone.org"
              target="_blank"
              rel="noreferrer"
            >
              Plone Docs
            </a>
          </li>
          <li className="item">
            <a
              className="item"
              href="https://training.plone.org"
              target="_blank"
              rel="noreferrer"
            >
              Plone Training
            </a>
          </li>
          <li className="item">
            <a
              className="item"
              href="https://community.plone.org"
              target="_blank"
              rel="noreferrer"
            >
              Plone Community Forum
            </a>
          </li>
        </ul>
        <div className="logo">
          <a title="Site" href="/">
            <img
              src="/++resource++plone-logo.svg"
              alt="Plone Site"
              title="Plone Site"
            />
          </a>
        </div>
        <a
          className="powered-by"
          href="https://plone.org"
          target="_blank"
          rel="noreferrer"
        >
          Plone.org
        </a>
      </div>
    </>
  );
}

export default App;
