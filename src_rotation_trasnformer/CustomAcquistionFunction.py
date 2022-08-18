import torch
from torch import Tensor
from botorch.models.model import Model
from botorch.utils import t_batch_mode_transform
from botorch.acquisition import AnalyticAcquisitionFunction
from torch.distributions.normal import Normal

torch.backends.cudnn.allow_tf32 = False
torch.backends.cuda.matmul.allow_tf32 = False

class PrabuAcquistionFunction(AnalyticAcquisitionFunction):
    '''
        This class implements the acquisition function where we want to
        minimize the expectation of the modulus of the gradient of the
        objective function in a particular direction.
    '''
    def __init__(self, model: Model, maximize: bool = False) -> None:
        ''' 
            We use the AcquisitionFunction constructor, since that of 
            AnalyticAcquisitionFunction performs some validity checks 
            that we don't want here.
            
            Arguments:
            ---------
                - model: A BoTorch Model whose posterior will be used
                    to calculate the expectation.
                - maximize: (boolean) to describe whether we want to
                    minimize or maximize the acquisition function.
        '''
        
        super(AnalyticAcquisitionFunction, self).__init__(model)
        self.maximize = maximize
        
    def forward(self, X: Tensor) -> Tensor:
        '''
            This function calculates the value of the acquisition
            function at X.
            
            Arguments:
            ---------
                - X: (A PyTorch Tensor) Shape batch_size x q x d, where
                    d is the dimension of the input taken by the 
                    Objective Function

            Returns:
            -------
                PyTorch Tensor: A `(b)`-dim Tensor of Upper Confidence 
                    Bound values at the given design points `X`.
        '''
        torch.pi = torch.acos(torch.zeros(1)).item() * 2
        
        posterior = self.model.posterior(X)
        mean = posterior.mean.squeeze()
        covs = posterior.mvn.covariance_matrix.squeeze()
        sigma = torch.sqrt(covs)
        std_normal = Normal(torch.tensor([0.0]), torch.tensor([1.0]))
        pdf_value = (torch.exp(std_normal.log_prob(mean/sigma)))
        acq_value = (2*sigma*(1/torch.sqrt(torch.tensor(2*torch.pi)))*pdf_value 
            + mean*(1-2*std_normal.cdf(-mean/sigma)))

        if not self.maximize:
            acq_value = -acq_value
        
        return acq_value

    def get_name(self):
        return "PrabuAcquistionFunction"

class SumGradientAcquisitionFunction(AnalyticAcquisitionFunction):
    '''
    '''
    def __init__(self, model: Model, maximize: bool = False) -> None:
        ''' 
            We use the AcquisitionFunction constructor, since that of 
            AnalyticAcquisitionFunction performs some validity checks 
            that we don't want here.
            
            Arguments:
            ---------
                - model (list): A list BoTorch Model whose posterior 
                    will be used to calculate the expectation. In our
                    case this will be gradient gps along every 
                    dimension.
                - maximize: (boolean) to describe whether we want to
                    minimize or maximize the acquisition function.
        '''
        
        super(AnalyticAcquisitionFunction, self).__init__(model[0])
        self.grad_gps = model
        self.maximize = maximize
        
    def forward(self, X: Tensor) -> Tensor:
        '''
            This function calculates the value of the acquisition
            function at X.
            
            Arguments:
            ---------
                - X: (A PyTorch Tensor) Shape batch_size x q x d, where
                    d is the dimension of the input taken by the 
                    Objective Function
        '''
        acq_value = 0
        for grad_gp in self.grad_gps:
            acq_value += self.calculate_expected_partial_derivative(X, grad_gp)
        return acq_value

    def calculate_expected_partial_derivative(self, X, model):
        torch.pi = torch.acos(torch.zeros(1)).item() * 2
        
        posterior = model.posterior(X)
        mean = posterior.mean.squeeze()
        covs = posterior.mvn.covariance_matrix.squeeze()
        sigma = torch.sqrt(covs)
        std_normal = Normal(torch.tensor([0.0]), torch.tensor([1.0]))
        pdf_value = (torch.exp(std_normal.log_prob(mean/sigma)))
        acq_value = (2*sigma*(1/torch.sqrt(torch.tensor(2*torch.pi)))*pdf_value 
            + mean*(1-2*std_normal.cdf(-mean/sigma)))
        variance_term = mean**2 + sigma**2 - acq_value.detach().clone()**2
        acq_value += torch.sqrt(variance_term)

        if not self.maximize:
            acq_value = -acq_value

        return acq_value


class PIGradientAcquisitionFunction(AnalyticAcquisitionFunction):
    '''
    '''
    def __init__(self,obj_fn_gp,best_f,eps_values, model: Model, maximize: bool = False) -> None:
        ''' 
            We use the AcquisitionFunction constructor, since that of 
            AnalyticAcquisitionFunction performs some validity checks 
            that we don't want here.
            
            Arguments:
            ---------
                - model (list): A list BoTorch Model whose posterior 
                    will be used to calculate the expectation. In our
                    case this will be gradient gps along every 
                    dimension.
                - maximize: (boolean) to describe whether we want to
                    minimize or maximize the acquisition function.
        '''
        
        super(AnalyticAcquisitionFunction, self).__init__(model[0])
        self.obj_fn_gp = obj_fn_gp
        self.best_f = best_f
        self.grad_gps = model
        self.maximize = maximize
        self.eps_values = eps_values
        
    def forward(self, X: Tensor) -> Tensor:
        '''
            This function calculates the value of the acquisition
            function at X.
            
            Arguments:
            ---------
                - X: (A PyTorch Tensor) Shape batch_size x q x d, where
                    d is the dimension of the input taken by the 
                    Objective Function
        '''
        acq_value = 0
        acq_value += self.obj_fn_prob(X,self.obj_fn_gp,self.best_f)
        dim = 0
        for grad_gp in self.grad_gps:
            acq_value += self.calculate_expected_partial_derivative(X, grad_gp,dim)
            dim += 1
        return acq_value

    def obj_fn_prob(self,X,model,best_f):
        torch.pi = torch.acos(torch.zeros(1)).item() * 2
        eps = 0.1
        
        posterior = model.posterior(X)
        mean = posterior.mean.squeeze()
        covs = posterior.mvn.covariance_matrix.squeeze()
        sigma = torch.sqrt(covs)
        std_normal = Normal(torch.tensor([0.0]), torch.tensor([1.0]))
        acq_value = (std_normal.cdf((mean - best_f -eps)/sigma))

        acq_value[acq_value < 1e-40] = 1e-40

        acq_value = torch.log(acq_value)

        return acq_value

    def calculate_expected_partial_derivative(self, X, model,dim):

        torch.pi = torch.acos(torch.zeros(1)).item() * 2
        if self.eps_values[dim] > 0.1:
            eps = self.eps_values[dim]
        else:
            eps = 0.1
        
        posterior = model.posterior(X)
        mean = posterior.mean.squeeze()
        covs = posterior.mvn.covariance_matrix.squeeze()
        sigma = torch.sqrt(covs)
        std_normal = Normal(torch.tensor([0.0]), torch.tensor([1.0]))
        acq_value = (std_normal.cdf((eps - mean)/sigma) - 
                    std_normal.cdf(-(eps + mean)/sigma))
        acq_value[acq_value < 1e-40] = 1e-40

        acq_value = torch.log(acq_value)

        return acq_value

    def get_name(self):
        return "SumGradientAcquisitionFunction"