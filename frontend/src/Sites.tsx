import Badge from 'react-bootstrap/Badge';
import Card from 'react-bootstrap/Card';
import Button from 'react-bootstrap/Button';
import Col from 'react-bootstrap/Col';
import Row from 'react-bootstrap/Row';
import type { Site } from './queries';

const redirectSite = (href: string) => {
  window.location.href = href;
};

const SiteInfo = ({ site }: { site: Site }) => {
  const needUpgrade = site.needs_upgrade;
  return (
    <Card>
      <Card.Header>
        {site.id}
        {site.distribution && (
          <Badge pill bg={'success'} className={'float-end'}>
            {site.distribution}
          </Badge>
        )}
      </Card.Header>
      <Card.Body>
        <Card.Title>{site.title}</Card.Title>
        <Card.Text>{site.description}</Card.Text>
        <Button variant="primary" onClick={() => redirectSite(site['@id'])}>
          Visit
        </Button>
        {needUpgrade && (
          <button
            type="button"
            className="btn btn-warning"
            onClick={() => redirectSite(site['@id'])}
          >
            Upgrade
          </button>
        )}
      </Card.Body>
    </Card>
  );
};

const Sites = ({ sites }: { sites: Site[] }) => {
  return (
    sites && (
      <Row xs={1} md={2} className="g-4 sitesList">
        {sites.map((site, idx) => (
          <Col key={idx}>
            <SiteInfo site={site} />
          </Col>
        ))}
      </Row>
    )
  );
};

export default Sites;
