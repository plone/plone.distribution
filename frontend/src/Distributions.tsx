import { Distribution } from './queries';
import { Button } from '@plone/components';

type Handler = (can_manage: boolean, name: string) => Promise<void>;

const CustomBadge = ({ name }: { name?: string }) => {
  return <div className="distributionName">{name}</div>;
};

const CustomCard = ({
  title,
  description,
  name,
  image,
  buttonAction,
}: {
  title?: string;
  description?: string;
  name?: string;
  image?: string;
  buttonAction?: any;
}) => {
  return (
    <div className="kard">
      <div className="card-header">
        <h2>{title}</h2>
        <div className="badge-wrapper">
          <CustomBadge name={name} />
        </div>
      </div>

      <div className="main">
        {image && (
          <div className={'image-box'}>
            <img src={image} alt={title} />
          </div>
        )}
        <div className="hover-overlay">
          <p>{description}</p>
          <Button onPress={buttonAction}>Create</Button>
        </div>
      </div>
    </div>
  );
};

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
    <CustomCard
      title={distribution.title}
      description={distribution.description}
      image={distribution.image}
      buttonAction={() => handler(can_manage, distribution.name)}
      name={distribution.name}
    />
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
      <div className="distributionsList new">
        {distributions.map((distribution) => (
          <div key={distribution.name}>
            <DistributionCard
              distribution={distribution}
              handler={handler}
              can_manage={can_manage}
            />
          </div>
        ))}
      </div>
    )
  );
};

export default Distributions;
