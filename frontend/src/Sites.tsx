import type { Site } from './queries';
import { Button } from '@plone/components';

const redirectSite = (href: string) => {
  window.location.href = href;
};

const SiteInfo = ({ site }: { site: Site }) => {
  const CustomBadge = ({ name }: { name?: string }) => {
    return <div className="distributionName">{name}</div>;
  };

  const CustomCard = ({
    title,
    description,
    name,
    image,
    id,
    buttonAction,
    buttonText,
    distribution,
  }: {
    title?: string;
    description?: string;
    name?: string;
    image?: string;
    buttonAction?: any;
    id?: string;
    buttonText?: string;
    distribution?: string;
  }) => {
    return (
      <div className="kard">
        <div className="main">
          <div className="card-header">
            <div>
              <h2>{title}</h2>
              <span className="id">id: {name}</span>
            </div>

            <div className="badge-wrapper">
              <CustomBadge name={distribution} />
            </div>
          </div>

          {image && (
            <div className={'image-box'}>
              <img src={image} alt={title} />
            </div>
          )}
        </div>

        <div className="hover-overlay">
          <p>{description}</p>
          <Button onPress={buttonAction}>{buttonText}</Button>
        </div>
      </div>
    );
  };

  const needUpgrade = site.needs_upgrade;
  return (
    <CustomCard
      title={site.title}
      description={site.description}
      buttonAction={() => redirectSite(site['@id'])}
      name={site.id}
      buttonText={'Visit'}
      distribution={site.distribution}
    />
  );
};

const Sites = ({ sites }: { sites: Site[] }) => {
  return (
    sites && (
      <div className="sitesList">
        {sites.map((site, idx) => (
          <div key={idx}>
            <SiteInfo site={site} />
          </div>
        ))}
      </div>
    )
  );
};

export default Sites;
