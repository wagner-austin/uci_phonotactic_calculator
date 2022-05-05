from audioop import reverse
from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.views.generic.base import TemplateView
from django.urls import reverse_lazy
from webcalc_project import settings

from django.contrib import messages

from os import listdir
from os.path import isfile, join, basename

from src import ngram_calculator as calc
from src import validate

# Create your views here.
from .models import UploadTrain, DefaultFile, UploadWithDefault

class UploadTrainView(CreateView):
    model = UploadTrain
    fields = '__all__'#['training_file', 'test_file', 'training_model']
    template_name = 'home.html'
    success_url = reverse_lazy('output')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['documents'] = UploadTrain.objects.all() # change to self.model.objects.all() ?
        return context

    def form_invalid(self, form):
        response = super(UploadTrainView, self).form_invalid(form)
        context = self.get_context_data()
        form.data = form.data.copy()  # make copy of form data
        form.data['training_model'] = '' # reset training model dropdown selection in form
        context['form'] = form # set form in context to updated form
        messages.warning(self.request, 'Bad file formatting')
        return response

    def form_valid(self, form):
        response = super(UploadTrainView, self).form_valid(form)
        
        media_path = settings.MEDIA_ROOT
        train_file = join(media_path, 'uploads', basename((self.model.objects.last()).training_file.name))
        test_file = join(media_path, 'uploads', basename((self.model.objects.last()).test_file.name))

        # Validate training and test files here
        # If not valid, return form_invalid without calling run
        ###########

        if not validate.valid_file(train_file) or not validate.valid_file(test_file):
            return self.form_invalid(form)

        test_file_name_sub = ((self.model.objects.last()).test_file.name)[:4]
        old_outfile_name = (self.model.objects.last()).out_file
        new_outfile_name = old_outfile_name.replace('.csv', '') + '_' + test_file_name_sub + '.csv'

        out_file = join(media_path, 'uploads', basename(new_outfile_name))
        calc.run(train_file, test_file, out_file)
        return response

class MediaView(TemplateView):
    template_name = 'media.html'
    model = DefaultFile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #media_path = join(settings.MEDIA_ROOT, 'default')
        #files = [f for f in listdir(media_path) if isfile(join(media_path, f))]
        #context['myfiles'] = files
        context['objects'] = self.model.objects.all()
        return context

class OutputView(TemplateView):
    model = UploadTrain
    #fields = ['training_file', test]
    template_name = 'output.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        test_file_name_sub = basename((self.model.objects.last()).test_file.name)[:4]
        old_outfile_name = (self.model.objects.last()).out_file
        new_outfile_name = old_outfile_name.replace('.csv', '') + '_' + test_file_name_sub + '.csv'

        context['output_file'] = new_outfile_name#(self.model.objects.last()).out_file
        return context

class AboutView(TemplateView):
    template_name = 'about.html'


class UploadDefaultView(CreateView):
    model = UploadWithDefault
    fields = '__all__'
    template_name = 'uploadDefault.html'
    success_url = reverse_lazy('output')

    def form_invalid(self, form):
        response = super(UploadDefaultView, self).form_invalid(form)
        context = self.get_context_data()
        form.data = form.data.copy()  # make copy of form data
        form.data['training_model'] = '' # reset training model dropdown selection in form
        form.data['training_file'] = '' # reset training file dropdown selection in form
        context['form'] = form # set form in context to updated form
        messages.warning(self.request, 'Bad file formatting')
        return response

    def form_valid(self, form):
        response = super(UploadDefaultView, self).form_valid(form)

        media_path = settings.MEDIA_ROOT
        
        train_file = join(media_path, 'default', basename((self.model.objects.last()).training_file))
        test_file = join(media_path, 'uploads', basename((self.model.objects.last()).test_file.name))

        # Validate test file here
        # If not valid, return form_invalid without calling run
        # No need to validate training file since it is default file
        ###########

        if not validate.valid_file(test_file):
            return self.form_invalid(form)

        test_file_name_sub = basename((self.model.objects.last()).test_file.name)[:4]
        old_outfile_name = (self.model.objects.last()).out_file
        new_outfile_name = old_outfile_name.replace('.csv', '') + '_' + test_file_name_sub + '.csv'

        out_file = join(media_path, 'uploads', basename(new_outfile_name))
        calc.run(train_file, test_file, out_file)
        return response

class OutputDefaultView(TemplateView):
    model = UploadWithDefault
    #fields = ['training_file', test]
    template_name = 'output.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        print(basename((self.model.objects.last()).test_file.name), ((self.model.objects.last()).test_file.name))
        test_file_name_sub = basename((self.model.objects.last()).test_file.name)[:4]
        old_outfile_name = (self.model.objects.last()).out_file
        new_outfile_name = old_outfile_name.replace('.csv', '') + '_' + test_file_name_sub + '.csv'
        print(test_file_name_sub, old_outfile_name, new_outfile_name)

        context['output_file'] = new_outfile_name#(self.model.objects.last()).out_file
        return context
