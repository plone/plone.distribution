import { RJSFSchema, UiSchema } from '@rjsf/utils';

export type Distribution = {
  '@id': string;
  name: string;
  description: string;
  title: string;
  image: string;
};

export type Site = {
  '@id': string;
  id: string;
  description: string;
  title: string;
  needs_upgrade: string;
};

type SitesEndpoint = {
  '@id': string;
  distributions: Distribution[];
  sites: Site[];
  can_manage: boolean;
};

export type SitesEndpointDistributionDetail = {
  '@id': string;
  name: string;
  description: string;
  title: string;
  image: string;
  uischema: UiSchema;
  schema: RJSFSchema;
  default_values: {
    site_id: string;
    default_language: string;
  };
};

const getDistributions = async (): Promise<SitesEndpoint> => {
  const response = await fetch('/@sites', {
    headers: {
      Accept: 'application/json',
    },
  });
  if (!response.ok) {
    throw new Error('Network response was not ok');
  }
  return response.json();
};

export const getDistributionsQuery = () => ({
  queryKey: ['distributions'],
  queryFn: async () => getDistributions(),
});

const getDistribution = async (
  name: string,
): Promise<SitesEndpointDistributionDetail> => {
  const response = await fetch('/@sites/' + name, {
    headers: {
      Accept: 'application/json',
    },
  });
  if (!response.ok) {
    throw new Error('Network response was not ok');
  }
  return response.json();
};

export const getDistributionQuery = (name: string) => ({
  queryKey: ['distribution', name],
  queryFn: async () => getDistribution(name),
  select: (data: SitesEndpointDistributionDetail) => {
    const { timeZone } = Intl.DateTimeFormat().resolvedOptions();
    const newData = {
      ...data,
      schema: {
        ...data.schema,
        definitions: {
          ...data.schema.definitions,
          // We detect the current timezone and inject it in the returned object
          // instead of the default
          timezones: {
            // @ts-ignore
            ...data.schema.definitions.timezones!,
            default: timeZone,
          },
        },
        properties: {
          ...data.schema.properties,
          // Populate with the suggested site_id from the backend request
          site_id: {
            // @ts-ignore
            ...data.schema.properties.site_id,
            default: data.default_values.site_id,
          },
          default_language: {
            // @ts-ignore
            ...data.schema.properties.default_language,
            default: data.default_values.default_language,
          },
        },
      },
    };
    return newData;
  },
});
