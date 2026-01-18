import argparse
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


def plot_file(file_path: str, flip: bool = False, save_img: str | None = None):
    df = pd.read_excel(file_path)

    # Ensure column names are strings to avoid matplotlib type errors
    df.columns = df.columns.map(str)

    # Remove rows and columns that are completely empty
    df = df.dropna(how='all', axis=0)
    df = df.dropna(how='all', axis=1)

    # Display the data if it's not empty
    if df.empty:
        print("No data found in the Excel file.")
        return

    # Try to interpret the first column as dates for the horizontal axis
    x_dates = None
    dates_flag = False
    if df.shape[1] >= 1:
        x_try = pd.to_datetime(df.iloc[:, 0], errors='coerce', infer_datetime_format=True)
        if x_try.notna().any():
            x_dates = x_try
            dates_flag = True

    if flip:
        # Swapped axes: current behavior (y on x-axis, x on y-axis)
        title = 'Swapped Axes Plot'
        if df.shape[1] == 1:
            # Single column: treat as y-values and swap axes when plotting
            y = pd.to_numeric(df.iloc[:, 0], errors='coerce')
            x = pd.Series(range(len(y)))
            plot_x = y.dropna().values
            plot_y = x.loc[y.dropna().index].values
            if plot_x.size == 0:
                raise SystemExit("No numeric data available to plot.")
            plt.plot(plot_x, plot_y, marker='o', linestyle='-')
            plt.xlabel(str(df.columns[0]))
            plt.ylabel('Index')
        else:
            # Multiple columns: first column is original x, remaining are y series.
            x_raw = df.iloc[:, 0]
            # if first column parsed as dates, use those for the (vertical) axis when flipped
            if dates_flag:
                x_vals = x_dates
            else:
                x_num = pd.to_numeric(x_raw, errors='coerce')
                use_index = x_num.isna().all()
                if use_index:
                    x_vals = pd.Series(range(len(df)))
                else:
                    x_vals = x_num

            any_plotted = False
            for col in df.columns[1:]:
                y_num = pd.to_numeric(df[col], errors='coerce')
                if use_index:
                    valid_idx = y_num.dropna().index
                else:
                    valid_idx = y_num.dropna().index.intersection(x_vals.dropna().index)

                if len(valid_idx) == 0:
                    continue
                plt.plot(y_num.loc[valid_idx].values, x_vals.loc[valid_idx].values, marker='o', linestyle='-', label=str(col))
                any_plotted = True

            if not any_plotted:
                raise SystemExit("No numeric series found to plot.")

            plt.xlabel('y')
            plt.ylabel(str(df.columns[0]))
            plt.legend()
            # If we used dates for the vertical axis (flip mode) format y-axis as dates
            if dates_flag:
                ay = plt.gca()
                locator = mdates.AutoDateLocator()
                fmt = mdates.ConciseDateFormatter(locator)
                ay.yaxis.set_major_locator(locator)
                ay.yaxis.set_major_formatter(fmt)
    else:
        # Normal axes: numbers like 80/81 go to vertical axis (y)
        title = 'Line Plot (values on vertical axis)'
        if df.shape[1] == 1:
            x = range(len(df))
            y = pd.to_numeric(df.iloc[:, 0], errors='coerce')
            y_plot = y.dropna().values
            x_plot = [i for i in range(len(y)) if not pd.isna(y.iloc[i])]
            if len(y_plot) == 0:
                raise SystemExit("No numeric data available to plot.")
            plt.plot(x_plot, y_plot, marker='o', linestyle='-')
            plt.xlabel('Index')
            plt.ylabel(str(df.columns[0]))
        else:
            x_raw = df.iloc[:, 0]
            # prefer dates for horizontal axis when available
            if dates_flag:
                x_vals = x_dates
            else:
                x_num = pd.to_numeric(x_raw, errors='coerce')
                if x_num.isna().all():
                    x_vals = range(len(df))
                else:
                    x_vals = x_num

            any_plotted = False
            for col in df.columns[1:]:
                y_num = pd.to_numeric(df[col], errors='coerce')
                valid_idx = y_num.dropna().index.intersection(pd.Index(range(len(df))))
                if len(valid_idx) == 0:
                    continue
                plt.plot([x_vals[i] for i in valid_idx], y_num.loc[valid_idx].values, marker='o', linestyle='-', label=str(col))
                any_plotted = True

            if not any_plotted:
                raise SystemExit("No numeric series found to plot.")
            plt.xlabel(str(df.columns[0]))
            plt.ylabel('y')
            plt.legend()
            # If horizontal axis uses dates, format x-axis accordingly
            if dates_flag:
                ax = plt.gca()
                locator = mdates.AutoDateLocator()
                fmt = mdates.ConciseDateFormatter(locator)
                ax.xaxis.set_major_locator(locator)
                ax.xaxis.set_major_formatter(fmt)
                plt.gcf().autofmt_xdate()

    plt.title(title)
    plt.tight_layout()
    plt.grid(True, alpha=0.3)
    if save_img:
        plt.savefig(save_img, bbox_inches='tight')
        print(f"Saved plot to {save_img}")
    plt.show()


def parse_args():
    p = argparse.ArgumentParser(description='Plot data from Excel with option to flip axes')
    p.add_argument('--file', '-f', default='data.xlsx', help='Path to Excel file (default data.xlsx)')
    p.add_argument('--flip', action='store_true', help='Flip axes so numeric values appear on vertical axis')
    p.add_argument('--save-img', help='Save the pyplot figure to this image path')
    return p.parse_args()


if __name__ == '__main__':
    args = parse_args()
    plot_file(args.file, flip=args.flip, save_img=args.save_img)