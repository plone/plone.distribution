import type { Site } from './queries';

const Sites = ({ sites }: { sites: Site[] }) => {
  return (
    <div className="list-group">
      {sites.map((site) => (
        <a
          href={site['@id']}
          className="list-group-item list-group-item-action"
          aria-current="true"
          key={site['@id']}
        >
          <div className="d-flex w-100 justify-content-between">
            <h5 className="mb-1">{site.id}</h5>
            {site.needs_upgrade && (
              // TODO: link to the site upgrade
              <h5>
                <span className="badge bg-primary">Upgrade</span>
              </h5>
            )}
          </div>
          <p className="mb-1">{site.description}</p>
          {/* <small></small> */}
        </a>
      ))}
    </div>
  );
};

export default Sites;
