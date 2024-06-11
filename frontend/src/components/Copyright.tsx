import { Typography } from "@mui/material";
import Link from '@mui/material/Link';

export default function Copyright(props: any) {
    return (
      <Typography variant="body2" sx={{mt: 5}} color="text.secondary" align="center" {...props}>
        {'Copyright © '}
        <Link color="inherit" href="https:/grandline.com">
          Grand Line
        </Link>{' '}
        {new Date().getFullYear()}
        {'.'}
      </Typography>
    );
  }