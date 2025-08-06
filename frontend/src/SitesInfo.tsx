import { useQuery } from '@tanstack/react-query';
import { useState } from 'react';
import { createPortal } from 'react-dom';
import { getDistributionsQuery } from './queries';
import Distributions from './Distributions';
import Sites from './Sites';
import LoginModal from './LoginModal';
import { Portal } from 'react-portal';
import { Button } from '@plone/components';

const SitesInfo = () => {
  const { isLoading, isError, data, error } = useQuery(getDistributionsQuery());
  const [showLoginModal, setShowLoginModal] = useState(false);
  const [cameFrom, setCameFrom] = useState('');

  const checkBasicAuth = async () => {
    const response = await fetch('@@ploneAddSite', {
      method: 'GET',
    });
    if (response.status === 401) {
      return false;
    }
    setShowLoginModal(false);
    return true;
  };

  const handleClick = async (can_manage: boolean, name: string) => {
    const href = import.meta.env.PROD
      ? `@@ploneAddSite?distribution=${name}`
      : `?distribution=${name}`;
    if (can_manage) {
      // Redirect
      window.location.href = href;
    } else {
      setCameFrom(href);
      if (await checkBasicAuth()) {
        window.location.href = href;
      } else {
        setShowLoginModal(true);
      }
    }
  };

  if (isLoading) return <>Loading...</>;

  if (isError) return <>{'An error has occurred: ' + error}</>;

  if (data) {
    const { sites, distributions, can_manage } = data;
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
        {sites?.length > 0 ? (
          <div className={'sites'}>
            <h2>Sites</h2>
            <hr />
            <h3>Existing Sites</h3>
            <Sites sites={sites} />
          </div>
        ) : null}
        {distributions?.length > 0 ? (
          <div className={'distributions'}>
            <h2>Create a new site</h2>
            <hr />
            <h3>Available distributions</h3>
            <Distributions
              distributions={distributions}
              can_manage={can_manage}
              handler={handleClick}
            />
          </div>
        ) : null}
        {!can_manage &&
          createPortal(
            <Button
              type="button"
              className="btn btn-primary"
              onPress={() => checkBasicAuth()}
            >
              Login
            </Button>,
            document.getElementById('topForm') as HTMLElement,
          )}
      </>
    );
  }
  return null;
};

export default SitesInfo;
