import React, { useState } from 'react';
import Box from '@mui/material/Box';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select, { SelectChangeEvent } from '@mui/material/Select';

type Props = {
  variants: any | null;
  onSelectPick: any;
};

export default function BasicSelect(props: Props) {
  const [picked, setPicked] = useState('');
  const { variants, onSelectPick } = props;

  const handleChange = (event: SelectChangeEvent) => {
    setPicked(event.target.value as string);
    onSelectPick(event);
  };

  return (
    <Box sx={{ minWidth: 120 }}>
      <FormControl fullWidth>
        <InputLabel id="demo-simple-select-label">Age</InputLabel>
        <Select
          labelId="demo-simple-select-label"
          id="demo-simple-select"
          value={picked}
          label="Trading tool"
          autoWidth
          onChange={handleChange}
        >
          {variants.map((val: string) => {
            return (
              <MenuItem key={val} value={val}>
                {val}
              </MenuItem>
            );
          })}
        </Select>
      </FormControl>
    </Box>
  );
}
