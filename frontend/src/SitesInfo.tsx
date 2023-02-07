import { useQuery } from '@tanstack/react-query';
import { useState } from 'react';
import { createPortal } from 'react-dom';
import { getDistributionsQuery } from './queries';
import Sites from './Sites';
import LoginModal from './LoginModal';
import { Portal } from 'react-portal';

const SitesInfo = () => {
  const { isLoading, isError, data, error } = useQuery(getDistributionsQuery());
  const [showLoginModal, setShowLoginModal] = useState(false);
  const [cameFrom, setCameFrom] = useState('');

  const handleClick = (can_manage: boolean, name: string) => {
    const href = `/?distribution=${name}`;
    if (can_manage) {
      // Redirect
      window.location.href = href;
    } else {
      setCameFrom(href);
      setShowLoginModal(true);
    }
  };

  if (isLoading) return <>Loading...</>;

  if (isError) return <>{'An error has occurred: ' + error}</>;

  if (data) {
    const { sites, can_manage } = data;
    return (
      <>
        {showLoginModal && (
          <Portal>
            <LoginModal
              cameFrom={cameFrom}
              closeModalHandler={() => setShowLoginModal(false)}
            />
          </Portal>
        )}
        <h1>Plone is up and running.</h1>
        <Sites sites={sites} />
        <h2 className="my-4">Create a new site using a distribution:</h2>
        {data?.distributions ? (
          <div className="row">
            {data.distributions.map((distribution) => (
              <div className="col-sm-4" key={distribution.name}>
                <div className="card">
                  <img
                    src={distribution.image}
                    className="card-img-top"
                    alt=""
                  />
                  <div className="card-body">
                    <h5 className="card-title">{distribution.title}</h5>
                    <p className="card-text">{distribution.description}</p>
                    <button
                      type="button"
                      className="btn btn-primary"
                      onClick={() => handleClick(can_manage, distribution.name)}
                    >
                      Create
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        ) : null}
        {!can_manage &&
          createPortal(
            <button
              type="button"
              className="btn btn-primary"
              onClick={() => setShowLoginModal(true)}
            >
              Login
            </button>,
            document.getElementById('topForm') as HTMLElement,
          )}
      </>
    );
  }
  return null;
};

export default SitesInfo;
