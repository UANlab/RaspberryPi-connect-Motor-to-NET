

tic

LB = [ 0  0 -0.04];
UB = [0.8 10 0];

GA_options = optimoptions( 'ga',...
                     'Display','iter', ...
                     'MaxGenerations',70,...
                     'PopulationSize',100,...
                     'PlotFcns',{@gaplotbestf,@kp_plot,@ki_plot, @kd_plot},...
                     'CrossoverFraction',0.8,...
                      'MutationFcn', {@mutationuniform, 0.1});

[x, fval] = ga(@CostFunction, 3, [], [], [], [], LB, UB, [], [], GA_options)

toc

function IAE = CostFunction(x)

%     s = tf('s');
%     system = (2.757*s + 0.6607) / (s^2 + 4.647*s + 0.6626);
    kp = x(1);
    ki = x(2);
    kd = x(3);
    
    simIn = Simulink.SimulationInput('GA_Simu');
    simIn = setVariable(simIn,'SimuKp',kp);
    simIn = setVariable(simIn,'SimuKi',ki);
    simIn = setVariable(simIn,'SimuKd',kd);
    simOutputs = sim(simIn);
    dt = 0.00001;
    edt = abs(simOutputs.simout.signals.values - 1) * dt;
    if sum(edt(:)) > 10
        IAE = 10
%     elseif max(simOutputs.simout.signals.values) > 1.07 % Overshoot限制
%         IAE = 2
    elseif min(simOutputs.simout.signals.values) < -0.1 % Response不能負太多
        IAE = 5
    else
    IAE_i = sum(edt(:));
        if max(simOutputs.simout.signals.values) > 1.07
            IAE = IAE_i + (max(simOutputs.simout.signals.values) - 1.07)*5  % Overshoot加權
        else
            IAE = IAE_i
        end
    end
%     PID_controller = kp + ki/s + kd*s;
% 
%     close_system = feedback(PID_controller * system , 1);
%     dt = 0.1;        %解析度
%     t = [0:dt:10];

%     [y,t] = step(close_system, t);
% 
%     edt = abs(1-y) * dt;
% 
%     IAE = sum(edt);
end

function state = kp_plot(GA_options, state, flag)
    UB = [0.9 10 0];
    kp = state.Population(:,1);
    kp_mean = mean(kp(:));
    hold on;
    plot(state.Generation, kp_mean,'.red')
    xlabel('Generation','interp','none');
    ylabel('Kp','interp','none');
    if state.Generation ~= 0
        target = find(state.Score == state.Best(state.Generation));
        kp_best = state.Population(target(1),1);
        plot(state.Generation, kp_best,'.black')
    else
        kp_best = 0;
    end
    set(gca, 'XLim', [0, 70], 'XTick', 0:20:70,...
    'XTickLabel', 0:20:70);
    set(gca, 'YLim', [0, (UB(1)+1)], 'YTick', 0:((UB(1)+1)/5):(UB(1)+1),...
    'YTickLabel', 0:((UB(1)+1)/5):(UB(1)+1));
    tit = "Best:%g  Mean:%g";
    sprintf(tit,kp_best, kp_mean);
     set(get(gca,'Title'),'String',sprintf(tit,kp_best, kp_mean));
    hold off;
end

function state = ki_plot(GA_options, state, flag)
    UB = [0.9 10 0];
    ki = state.Population(:,2);
    ki_mean = mean(ki);
    hold on;
    plot(state.Generation, ki_mean,'.red')
    xlabel('Generation','interp','none');
    ylabel('Ki','interp','none');
    if state.Generation ~= 0
        target = find(state.Score == state.Best(state.Generation));
        ki_best = state.Population(target(1),2);
        plot(state.Generation, ki_best,'.black')
    else
        ki_best = 0;
    end
   set(gca, 'XLim', [0, 70], 'XTick', 0:20:70,...
    'XTickLabel', 0:20:70);
    set(gca, 'YLim', [0, (UB(2)+2)], 'YTick', 0:((UB(2)+1)/5):(UB(2)+2),...
    'YTickLabel', 0:((UB(2)+2)/5):(UB(2)+2));
    hold off;
    tit = "Best:%g  Mean:%g";
    sprintf(tit,ki_best, ki_mean);
     set(get(gca,'Title'),'String',sprintf(tit,ki_best, ki_mean));
end

function state = kd_plot(GA_options, state, flag)
    LB = [ 0.2  0.3 -0.04];
    kd = state.Population(:,3);
    kd_mean = mean(kd);
    hold on;
    plot(state.Generation, kd_mean,'.red')
    xlabel('Generation','interp','none');
    ylabel('Kd','interp','none');
    if state.Generation ~= 0
        target = find(state.Score == state.Best(state.Generation));
        kd_best = state.Population(target(1),3);
        plot(state.Generation, kd_best,'.black')
    else
        kd_best = 0;
    end
    set(gca, 'XLim', [0, 70], 'XTick', 0:20:70,...
    'XTickLabel', 0:20:70);
    set(gca, 'YLim', [(LB(3)-0.01), 0], 'YTick', (LB(3)-0.01):((LB(3)-0.01)/(-5)):0,...
    'YTickLabel', (LB(3)-0.01):((LB(3)-0.01)/(-5)):0);
    hold off;
    tit = "Best:%g  Mean:%g";
    sprintf(tit,kd_best, kd_mean);
     set(get(gca,'Title'),'String',sprintf(tit,kd_best, kd_mean));
end