import torch
"cuda" if torch.cuda.is_available() else "cpu"
import cupy as cp


def gauss_seidel_torch(f: torch.Tensor):
    """
    Applies the Gauss-Seidel method to solve a system of linear equations represented by the input tensor.

    Parameters:
    f (torch.Tensor): The input tensor representing the system of linear equations.

    Returns:
    torch.Tensor: The updated tensor after applying the Gauss-Seidel method.
    """
    newf = f.clone().detach()
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    newf = newf.to(device)
    newf[[-1,0],:] = 0
    newf[:,[-1,0]] = 0


    newf[1:-1, 1:-1] = 0.25 * (
            torch.roll(newf, 1, dims=0)[1:-1, 1:-1]
            + torch.roll(newf, -1, dims=0)[1:-1, 1:-1]
            + torch.roll(newf, 1, dims=1)[1:-1, 1:-1]
            + torch.roll(newf, -1, dims=1)[1:-1, 1:-1]
        )

    return newf


def gauss_seidel_cupy(f: cp.ndarray):
    """
    Applies the Gauss-Seidel method to solve a 2D array using the Cupy library.

    Args:
        f (cp.ndarray): The input 2D array.

    Returns:
        cp.ndarray: The updated 2D array after applying the Gauss-Seidel method.
    """
    newf = cp.array(f)
    newf[[-1,0],:] = 0
    newf[:,[-1,0]] = 0


    newf[1:-1, 1:-1] = 0.25 * (
            cp.roll(newf, 1, axis=0)[1:-1, 1:-1]
            + cp.roll(newf, -1, axis=0)[1:-1, 1:-1]
            + cp.roll(newf, 1, axis=1)[1:-1, 1:-1]
            + cp.roll(newf, -1, axis=1)[1:-1, 1:-1]
        )


    return newf