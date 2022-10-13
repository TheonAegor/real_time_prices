import * as React from 'react';
import Stack from '@mui/material/Stack';
import TextField from '@mui/material/TextField';

type Props = {
  value: number;
};

export default function BasicTextField(props: Props) {
  const { value } = props;

  return (
    <Stack
      component="form"
      sx={{
        width: '25ch',
      }}
      spacing={2}
      noValidate
      autoComplete="off"
    >
      <TextField
        hiddenLabel
        id="filled-hidden-label-normal"
        defaultValue="Normal"
        variant="filled"
        value={value}
        inputProps={{ readOnly: true }}
      />
    </Stack>
  );
}
