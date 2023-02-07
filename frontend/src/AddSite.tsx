import { useQuery } from '@tanstack/react-query';
import { DistributionsForm } from './DistributionsForm';
import { getDistributionQuery } from './queries';

const AddSite = ({ distribution }: { distribution: string }) => {
  const { isLoading, isError, data, error } = useQuery(
    getDistributionQuery(distribution),
  );

  return (
    <>
      {data ? (
        <DistributionsForm
          schema={data.schema}
          uiSchema={data.uischema}
          distribution={distribution}
        />
      ) : null}
    </>
  );
};

export default AddSite;
