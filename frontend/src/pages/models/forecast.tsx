import * as React from 'react';
import { LineChart, AnimatedLine, AnimatedLineProps } from '@mui/x-charts/LineChart';
import { useChartId, useDrawingArea, useXScale } from '@mui/x-charts/hooks';
import { SxProps, Theme } from '@mui/system';
import Predictions from '../../interfaces/predictions';
import { Box } from '@mui/system';

interface CustomAnimatedLineProps extends AnimatedLineProps {
  limit?: number;
  sxBefore?: SxProps<Theme>;
  sxAfter?: SxProps<Theme>;
}

function CustomAnimatedLine(props: CustomAnimatedLineProps) {
  const { limit, sxBefore, sxAfter, ...other } = props;
  const { top, bottom, height, left, width } = useDrawingArea();
  const scale = useXScale();
  const chartId = useChartId();

  if (limit === undefined) {
    return <AnimatedLine {...other} />;
  }

  const limitPosition = scale(limit); // Convert value to x coordinate.

  if (limitPosition === undefined) {
    return <AnimatedLine {...other} />;
  }

  const clipIdleft = `${chartId}-${props.ownerState.id}-line-limit-${limit}-1`;
  const clipIdRight = `${chartId}-${props.ownerState.id}-line-limit-${limit}-2`;
  return (
    <React.Fragment>
      {/* Clip to show the line before the limit */}
      <clipPath id={clipIdleft}>
        <rect
          x={left}
          y={0}
          width={limitPosition - left}
          height={top + height + bottom}
        />
      </clipPath>
      {/* Clip to show the line after the limit */}
      <clipPath id={clipIdRight}>
        <rect
          x={limitPosition}
          y={0}
          width={left + width - limitPosition}
          height={top + height + bottom}
        />
      </clipPath>
      <g clipPath={`url(#${clipIdleft})`}>
        <AnimatedLine {...other} sx={sxBefore} />
      </g>
      <g clipPath={`url(#${clipIdRight})`}>
        <AnimatedLine {...other} sx={sxAfter} />
      </g>
    </React.Fragment>
  );
}

interface ForecastProps extends Predictions {
  loading: boolean;
}

export default function Forecast(props: ForecastProps) {
  const combined = props.history.concat(props.predictions)
  const dates = combined.map(m => new Date(m.date));
  const prices = combined.map(m => m.price);
  const limitIndex = props.history.length - 1;

  console.log(combined);
  console.log(dates);
  console.log(prices);

  if (props.loading) {
    return <div>Loading...</div>;
  }

  return (
    <Box sx={{ width: '100%', height: '100%' }}>
      <LineChart
        series={[
          {
            type: 'line',
            label: "Price",
            data: prices,
            valueFormatter: (v, i) => `${v}${i.dataIndex > limitIndex ? ' (estimated)' : ''}`,
          },
        ]}
        xAxis={[
          { 
            data: dates,
            label: "Date",
            valueFormatter: (value) => new Date(value).toLocaleDateString(),
          }
        ]}
        height={400}
        slots={{ line: CustomAnimatedLine }}
        slotProps={{ line: { limit: limitIndex, sxAfter: { strokeDasharray: '2 1', stroke: 'orange' } } as any }}
      />
    </Box>
  );
}
