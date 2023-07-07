import Badge from 'react-bootstrap/Badge';
import Card from 'react-bootstrap/Card';
import Button from 'react-bootstrap/Button';
import Col from 'react-bootstrap/Col';
import Row from 'react-bootstrap/Row';
import { Distribution } from './queries';

type Handler = (can_manage: boolean, name: string) => Promise<void>;

const DistributionCard = ({
  distribution,
  can_manage,
  handler,
}: {
  distribution: Distribution;
  can_manage: boolean;
  handler: Handler;
}) => {
  return (
    <Card>
      <div className={'image-box'}>
        <Badge pill bg={'success'} className={'distributionName'}>
          {distribution.name}
        </Badge>
        <Card.Img src={distribution.image} alt={distribution.title} />
      </div>
      <Card.Body>
        <Card.Title>{distribution.title}</Card.Title>
        <Card.Text>{distribution.description}</Card.Text>
        <Button
          variant="primary"
          onClick={() => handler(can_manage, distribution.name)}
        >
          Create
        </Button>
      </Card.Body>
    </Card>
  );
};

const Distributions = ({
  distributions,
  can_manage,
  handler,
}: {
  distributions: Distribution[];
  can_manage: boolean;
  handler: Handler;
}) => {
  return (
    distributions && (
      <Row xs={1} md={2} className="g-4 distributionsList">
        {distributions.map((distribution) => (
          <Col key={distribution.name}>
            <DistributionCard
              distribution={distribution}
              handler={handler}
              can_manage={can_manage}
            />
          </Col>
        ))}
      </Row>
    )
  );
};

export default Distributions;
