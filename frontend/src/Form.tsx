import { useState } from 'react';
import { RJSFSchema, UiSchema, ErrorSchema } from '@rjsf/utils';
import validator from '@rjsf/validator-ajv8';
import Form from '@rjsf/bootstrap-4';
import './form.css';

const FormGenerator = ({
  schema,
  uiSchema,
  extraErrors,
  onSubmit,
}: {
  schema: RJSFSchema;
  uiSchema?: UiSchema;
  extraErrors?: ErrorSchema;
  onSubmit: any;
}) => {
  const [formData, setData] = useState({});

  function onChange({ formData }: { formData: any }) {
    setData(formData);
  }

  return (
    <>
      <Form
        schema={schema}
        uiSchema={uiSchema}
        validator={validator}
        showErrorList={'top'}
        // @ts-ignore
        onChange={onChange}
        formData={formData}
        onSubmit={onSubmit}
        extraErrors={extraErrors}
      />
    </>
  );
};

export default FormGenerator;
