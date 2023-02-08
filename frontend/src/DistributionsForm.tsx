import { useState } from 'react';
import { RJSFSchema, UiSchema } from '@rjsf/utils';
import { customizeValidator } from '@rjsf/validator-ajv8';
import Ajv2019 from 'ajv/dist/2019';
import Form from '@rjsf/bootstrap-4';
import './form.css';

const validator = customizeValidator({ AjvClass: Ajv2019 });

export const DistributionsForm = ({
  schema,
  uiSchema,
  distribution,
}: {
  schema: RJSFSchema;
  uiSchema: UiSchema;
  distribution: string;
}) => {
  const [formData, setData] = useState({});

  function onChange({ formData }: { formData: any }) {
    setData(formData);
  }

  async function onSubmit(value: any) {
    const response = await fetch('/@sites', {
      method: 'POST',
      headers: {
        Accept: 'application/json',
      },
      body: JSON.stringify({ ...value.formData, distribution }),
    });

    if (response.ok) {
      const responseData = await response.json();
      window.location.replace(responseData['@id']);
    }
  }

  return (
    <>
      <a href="/">Back</a>
      <Form
        schema={schema}
        uiSchema={uiSchema}
        validator={validator}
        // @ts-ignore
        onChange={onChange}
        formData={formData}
        onSubmit={onSubmit}
      />
    </>
  );
};
