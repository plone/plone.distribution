import { useState } from 'react';
import { useMutation } from '@tanstack/react-query';
import { addSite } from './queries';
import { RJSFSchema, UiSchema } from '@rjsf/utils';
import { customizeValidator } from '@rjsf/validator-ajv8';
import Ajv2019 from 'ajv/dist/2019';
import Form from '@rjsf/bootstrap-4';
import Toast from 'react-bootstrap/Toast';
import './form.css';

type Handler = () => void;

const validator = customizeValidator({ AjvClass: Ajv2019 });

const ErrorToast = ({
  message,
  cleanFn,
}: {
  message: string;
  cleanFn: Handler;
}) => {
  return (
    <Toast onClose={cleanFn} className={'text-bg-danger border-danger'}>
      <Toast.Header>
        <strong className="me-auto">Error</strong>
        <small className="text-muted">just now</small>
      </Toast.Header>
      <Toast.Body>{message}</Toast.Body>
    </Toast>
  );
};

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
  const [errorMsg, setErrorMsg] = useState('');
  const mutation = useMutation({
    mutationFn: addSite,
  });

  function onChange({ formData }: { formData: any }) {
    setData(formData);
  }
  const clearError = () => {
    setErrorMsg('');
    mutation.reset();
  };

  async function onSubmit(value: any) {
    const body = { ...value.formData, distribution };
    mutation.mutate(body);
  }

  if (mutation.isSuccess) {
    const site_url = mutation.data['@id'];
    window.location.replace(site_url);
  }
  if (mutation.isError && !errorMsg) {
    const data = mutation.error.response.data;
    const msg = data.message ? data.message : data.type;
    setErrorMsg(msg);
    console.log(msg);
  }
  const containerClassName = mutation.isLoading
    ? 'loading'
    : mutation.isError
    ? 'error'
    : 'active';

  return (
    <div id="add-site-form" className={containerClassName}>
      <div className="spinner-border text-primary" role="status">
        <span className="visually-hidden">Loading...</span>
      </div>
      {mutation.isError && (
        <ErrorToast cleanFn={clearError} message={errorMsg} />
      )}
      <Form
        schema={schema}
        uiSchema={uiSchema}
        validator={validator}
        // @ts-ignore
        onChange={onChange}
        formData={formData}
        onSubmit={onSubmit}
      />
    </div>
  );
};
