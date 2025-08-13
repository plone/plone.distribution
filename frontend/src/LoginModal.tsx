import { RJSFSchema, UiSchema } from '@rjsf/utils';
import { useState } from 'react';
import Form from './Form';

const loginSchema: RJSFSchema = {
  properties: {
    login: {
      type: 'string',
      title: 'Username',
    },
    password: {
      type: 'string',
      title: 'Password',
    },
  },
  required: ['login', 'password'],
};

const uiLoginSchema: UiSchema = {
  'ui:order': ['login', 'password'],
};

const LoginModal = ({
  closeModalHandler,
  cameFrom,
}: {
  closeModalHandler: any;
  cameFrom: string;
}) => {
  const [extraErrors, setExtraErrors] = useState({});

  async function onSubmit(value: any) {
    const response = await fetch('@login', {
      method: 'POST',
      headers: {
        Accept: 'application/json',
      },
      body: JSON.stringify(value.formData),
    });

    if (response.ok) {
      setExtraErrors({});
      if (cameFrom) {
        window.location.href = cameFrom;
      }
      closeModalHandler();
    } else {
      setExtraErrors({
        __errors: ['Login or password are incorrect'],
      });
    }
  }

  return (
    <div className="modal fade show" style={{ display: 'block' }} tabIndex={-1}>
      <div className="modal-dialog">
        <div className="modal-content">
          <div className="modal-header">
            <h5 className="modal-title">Login Form</h5>
            <button
              type="button"
              className="btn-close"
              data-bs-dismiss="modal"
              aria-label="Close"
              onClick={closeModalHandler}
            ></button>
          </div>
          <div className="modal-body">
            <Form
              schema={loginSchema}
              uiSchema={uiLoginSchema}
              onSubmit={onSubmit}
              extraErrors={extraErrors}
            />
          </div>
        </div>
      </div>
    </div>
  );
};

export default LoginModal;
